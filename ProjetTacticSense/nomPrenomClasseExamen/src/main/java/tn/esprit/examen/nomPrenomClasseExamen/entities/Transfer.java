package tn.esprit.examen.nomPrenomClasseExamen.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.FieldDefaults;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
@FieldDefaults(level= AccessLevel.PRIVATE)
@Entity
public class Transfer {
    @Id
    @GeneratedValue
    private Long idTransfer;

        private String playerName;
    private String standardizedClub;
    @ManyToOne
    @JoinColumn(name = "idPlayer")
    private Player player;
}
