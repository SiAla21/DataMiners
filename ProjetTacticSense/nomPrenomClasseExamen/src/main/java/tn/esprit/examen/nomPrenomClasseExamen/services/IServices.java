package tn.esprit.examen.nomPrenomClasseExamen.services;

import org.springframework.web.multipart.MultipartFile;
import tn.esprit.examen.nomPrenomClasseExamen.entities.*;

import java.util.List;

public interface IServices {
    // PLAYER LOGIC
    Player getPlayerProfile(Long id);
    void requestVerification(Long playerId);
    public String verifyPlayer(MultipartFile[] images, String playerName, Long playerId);
    public String classifyImage(String imagePath);
        // CLUB LOGIC
    Club getClubProfile(Long id);
    Post createPost(Post post, Long clubId);
    List<User> getPostApplicants(Long postId);

    // POST + FEED LOGIC
    List<Post> getFeed();
    void applyToPost(Long postId, Long userId);

    // BLOGS
    List<Blog> getUserBlogs(Long userId);

    // RECOMMENDATIONS
    List<Club> recommendClubsForPlayer(Long playerId);
}
