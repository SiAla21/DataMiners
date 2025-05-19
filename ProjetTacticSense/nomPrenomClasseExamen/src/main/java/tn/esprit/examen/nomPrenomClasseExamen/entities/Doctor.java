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
public class Doctor extends User {

    String Rndrng_Prvdr_First_Name;

    String Rndrng_Prvdr_Last_Org_Name;

    String Rndrng_Prvdr_Type;

    int Tot_Benes ;

    float Bene_Avg_Age ;
}
