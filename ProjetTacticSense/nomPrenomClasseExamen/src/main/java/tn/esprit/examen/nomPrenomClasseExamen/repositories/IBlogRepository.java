package tn.esprit.examen.nomPrenomClasseExamen.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import tn.esprit.examen.nomPrenomClasseExamen.entities.Blog;
import tn.esprit.examen.nomPrenomClasseExamen.entities.Client;

public interface IBlogRepository extends JpaRepository<Blog, Long> {
}
