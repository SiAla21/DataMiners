package tn.esprit.examen.nomPrenomClasseExamen.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.*;
import lombok.experimental.FieldDefaults;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
@FieldDefaults(level= AccessLevel.PRIVATE)
@Entity
public class Player extends User{
    String team_name;
    String league;
    String name;
    String registered_position;
    Boolean IS_VERIFIED;
    float verification_score;
    int age;
    float speed;
    float acceleration;
    int dribbling;
    int ball_control;
    int low_pass;
    int finishing;
int defensive_awareness;
    int  physical_contact;
    int stamina;
     int kicking_power;
     int heading;
    int tight_possession;
}
