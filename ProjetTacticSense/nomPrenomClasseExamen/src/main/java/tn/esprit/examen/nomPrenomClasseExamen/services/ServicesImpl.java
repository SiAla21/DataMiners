package tn.esprit.examen.nomPrenomClasseExamen.services;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import tn.esprit.examen.nomPrenomClasseExamen.entities.*;
import tn.esprit.examen.nomPrenomClasseExamen.repositories.IClientRepository;
import tn.esprit.examen.nomPrenomClasseExamen.repositories.IPlayerRepository;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@RequiredArgsConstructor
@Service
public class ServicesImpl implements IServices {

IPlayerRepository playerRepository;
@Override
        public String verifyPlayer(MultipartFile[] images, String playerName, Long playerId) {
            try {
                if (images.length != 3) return "Exactly 3 images required";

                String basePath = "src/main/resources/tmp/";
                new File(basePath).mkdirs();
                List<String> paths = new ArrayList<>();

                for (int i = 0; i < 3; i++) {
                    String path = basePath + "selfie" + i + ".jpg";
                    images[i].transferTo(new File(path));
                    paths.add(path);
                }

                List<String> command = new ArrayList<>();
                command.add("python");
                command.add("src/main/resources/scripts/verif_system_final.py");
                command.add(playerName);
                command.addAll(paths);

                ProcessBuilder pb = new ProcessBuilder(command);
                pb.redirectErrorStream(true);
                Process process = pb.start();

                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                boolean verified = false;
                int score = 0;

                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("VERIFIED")) verified = Boolean.parseBoolean(line.split(" ")[1]);
                    if (line.startsWith("SCORE")) score = Integer.parseInt(line.split(" ")[1]);
                }

                process.waitFor();

                Player player = playerRepository.findById(playerId).orElseThrow();
                player.setIS_VERIFIED(verified);
                player.setVerification_score(score);
                playerRepository.save(player);

                // delete images
                for (String p : paths) new File(p).delete();

                return verified ? "✅ Verified (Score: " + score + ")" : "❌ Not Verified (Score: " + score + ")";
            } catch (Exception e) {
                e.printStackTrace();
                return "Error: " + e.getMessage();
            }
        }
    @Override
    public Player getPlayerProfile(Long id) {
        return null;
    }
    public String classifyImage(String imagePath) {
        try {
            // Path to Python executable and script
            String pythonPath = "python"; // or "python3" depending on your system
            String scriptPath = "C:/Users/bouaz/Classification_8classes.py";

            List<String> command = new ArrayList<>();
            command.add(pythonPath);
            command.add(scriptPath);
            command.add(imagePath);

            ProcessBuilder pb = new ProcessBuilder(command);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            // Read the output
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String output = reader.readLine(); // First line = prediction

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                return "Unknown"; // or handle error differently
            }

            return output != null ? output.trim() : "Unknown";

        } catch (Exception e) {
            e.printStackTrace();
            return "Unknown";
        }
    }
    @Override
    public void requestVerification(Long playerId) {

    }

    @Override
    public Club getClubProfile(Long id) {
        return null;
    }

    @Override
    public Post createPost(Post post, Long clubId) {
        return null;
    }

    @Override
    public List<User> getPostApplicants(Long postId) {
        return List.of();
    }

    @Override
    public List<Post> getFeed() {
        return List.of();
    }

    @Override
    public void applyToPost(Long postId, Long userId) {

    }

    @Override
    public List<Blog> getUserBlogs(Long userId) {
        return List.of();
    }

    @Override
    public List<Club> recommendClubsForPlayer(Long playerId) {
        return List.of();
    }
}
