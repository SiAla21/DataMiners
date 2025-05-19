package tn.esprit.examen.nomPrenomClasseExamen.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.FieldDefaults;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@ToString
@AllArgsConstructor
@NoArgsConstructor
@FieldDefaults(level= AccessLevel.PRIVATE)
@Entity
public class Club extends User{


    private String season;
    private Integer matchesPlayed;
    private Integer wins;
    private Integer draws;
    private Integer losses;
    private Integer goalsScored;
    private Integer goalsConceded;
    private Integer goalDifference;
    private Integer points;
    private String topScorer;
    private Integer cleanSheets;

    @Column(name = "possession_percent")
    private Double possessionPercent;

    @Column(name = "pass_accuracy_percent")
    private Double passAccuracyPercent;

    private Double shotsPerMatch;
    private Integer foulsCommitted;
    private Integer yellowCards;
    private Integer redCards;
    private Integer totalInjuries;
    private Integer recruitedPlayers;

    private Integer totalAttacksLeft;
    private Integer totalAttacksMiddle;
    private Integer totalAttacksRight;

    private Integer concededAttacksLeft;
    private Integer concededAttacksMiddle;
    private Integer concededAttacksRight;

    private String league;

    @Column(name = "possession_alt_percent")
    private Double possessionAltPercent;

    private String clubStandardizedX;
    private String matchedClub;
    private Long clubId;
    private String clubCode;
    private String name;

    private String domesticCompetitionId;
    private String totalMarketValue;
    private Integer squadSize;
    private Double averageAge;
    private Integer foreignersNumber;
    private String foreignersPercentage;
    private Integer nationalTeamPlayers;

    private String stadiumName;
    private Integer stadiumSeats;
    private String netTransferRecord;
    private String coachName;
    private String lastSeason;
    private String filename;
    private String url;
    private String clubStandardizedY;
    // One club has many posts
    @OneToMany(mappedBy = "club", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Post> posts = new ArrayList<>();

    // Many-to-many with players
    @ManyToMany
    @JoinTable(name = "post_players",
            joinColumns = @JoinColumn(name = "idPost"),
            inverseJoinColumns = @JoinColumn(name = "idPlayer"))
    private List<Player> players = new ArrayList<>();

    // Many-to-many with coaches
    @ManyToMany
    @JoinTable(name = "post_coaches",
            joinColumns = @JoinColumn(name = "idPost"),
            inverseJoinColumns = @JoinColumn(name = "idCoach"))
    private List<Coach> coaches = new ArrayList<>();

    // Many-to-many with doctors
    @ManyToMany
    @JoinTable(name = "post_doctors",
            joinColumns = @JoinColumn(name = "idPost"),
            inverseJoinColumns = @JoinColumn(name = "idDoctor"))
    private List<Doctor> doctors = new ArrayList<>();

}
