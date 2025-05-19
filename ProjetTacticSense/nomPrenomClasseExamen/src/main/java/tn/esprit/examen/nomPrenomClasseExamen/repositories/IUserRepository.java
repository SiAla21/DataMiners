package tn.esprit.examen.nomPrenomClasseExamen.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import tn.esprit.examen.nomPrenomClasseExamen.entities.Client;
import tn.esprit.examen.nomPrenomClasseExamen.entities.Player;
import tn.esprit.examen.nomPrenomClasseExamen.entities.User;

import java.util.List;

public interface IUserRepository extends JpaRepository<User, Long> {
public List<User> findByRole(int role);
}


