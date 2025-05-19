package tn.esprit.examen.nomPrenomClasseExamen.controllers;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import tn.esprit.examen.nomPrenomClasseExamen.entities.*;
import tn.esprit.examen.nomPrenomClasseExamen.repositories.*;
import tn.esprit.examen.nomPrenomClasseExamen.services.IServices;
import tn.esprit.examen.nomPrenomClasseExamen.services.ServicesImpl;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserRestController {
@Autowired
 ServicesImpl services;
       @Autowired
       private IUserRepository userRepository;
    @Autowired
    private IBlogRepository blogRepository;
    @Autowired
    private IPlayerRepository playerRepository;
    @Autowired
    private IDoctorRepository doctorRepository;
    @Autowired
    private IClubRepository clubRepository;
    @Autowired
    private ICoachRepository coachRepository;
    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping("/delete")
    public ResponseEntity<String> deleteImage(@RequestBody Map<String, String> body) {
        String path = body.get("path");
        if (path == null || path.isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid image path.");
        }

        File file = new File(path);
        if (file.exists() && file.delete()) {
            return ResponseEntity.ok("Image deleted successfully.");
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to delete image.");
        }
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping("/verify-player/{playerId}")
    public ResponseEntity<String> verifyPlayer(
            @PathVariable Long playerId,
            @RequestParam String playerName,
            @RequestParam List<String> images) {

        // Validate input
        if (playerName == null || playerName.trim().isEmpty()) {
            return ResponseEntity.badRequest().body("Player name is required");
        }

        if (images == null || images.size() != 3) {
            return ResponseEntity.badRequest().body("Exactly 3 image paths are required");
        }

        try {
            // Static reference path (e.g., scraped or stored image path)
            String referenceImage = "C:/images/officials/" + playerName + ".jpg";

            // Run your Python script with all paths
            ProcessBuilder pb = new ProcessBuilder(
                    "python",
                    "C:/Users/bouaz/verif_system_final.py",
                    playerName,
                    images.get(0),
                    images.get(1),
                    images.get(2),
                    referenceImage
            );

            pb.redirectErrorStream(true);
            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            process.waitFor();

            return ResponseEntity.ok(output.toString().trim());

        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Verification failed: " + e.getMessage());
        }
    }
    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping("/upload")
    public ResponseEntity<String> uploadImage(@RequestParam("image") MultipartFile image) {
        try {
            String userHome = System.getProperty("user.home");
            String downloadsPath = userHome + "/Downloads/";
            String fileName = "webcam_" + UUID.randomUUID() + ".jpg";

            Path filePath = Paths.get(downloadsPath + fileName);
            Files.write(filePath, image.getBytes());

            return ResponseEntity.ok(filePath.toString().replace("\\", "/"));
        } catch (IOException e) {
            return ResponseEntity.internalServerError().body("Upload failed: " + e.getMessage());
        }
    }

    @CrossOrigin(origins = "http://localhost:4200")
    @GetMapping("/players")
    public List<User> getAllPlayers() {
        int k=0;
        return userRepository.findByRole(k);
    }

    @CrossOrigin(origins = "http://localhost:4200")
    @PostMapping(value = "/blog/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<?> uploadBlog(@RequestParam("file") MultipartFile file,
                                        @RequestParam("description") String description,
                                        @RequestParam("userId") Long userId) {
        try {
            // Save uploaded image to disk
            String uploadDir = "uploads/";
            File dir = new File(uploadDir);
            if (!dir.exists()) dir.mkdirs();

            String imageName = System.currentTimeMillis() + "_" + file.getOriginalFilename();
            Path imagePath = Path.of(uploadDir, imageName);
            Files.copy(file.getInputStream(), imagePath, StandardCopyOption.REPLACE_EXISTING);

            // Run classification
            String label = services.classifyImage(imagePath.toString());

            // Check if it's a valid Category
            Category category;
            try {
                category = Category.valueOf(label);
            } catch (IllegalArgumentException e) {
                // Unknown category or low confidence: don't save
                return ResponseEntity.badRequest().body("Image not recognized as a valid category.");
            }

            // Create and save blog
            Blog blog = new Blog();
            blog.setDescription(description);
            blog.setImage(imageName); // Or save full path if needed
            blog.setCategory(category);
            blog.setUser(userRepository.findById(userId).orElseThrow());

            blogRepository.save(blog);
            return ResponseEntity.ok(blog);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error uploading blog.");
        }
    }
    @GetMapping("/doctors")
    public List<Doctor> getAllDoctors() {
        return doctorRepository.findAll();
    }

    @GetMapping("/clubs")
    public List<Club> getAllClubs() {
        return clubRepository.findAll();
    }

    @GetMapping("/coaches")
    public List<Coach> getAllCoach() {
        return coachRepository.findAll();
    }
}
