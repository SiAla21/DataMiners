import { Routes } from '@angular/router';
import { RecommenderComponent } from './recommender/recommender.component';
import { RonaldoProfileComponent } from './ronaldo-profile/ronaldo-profile.component';
import { ProfileComponent } from './player/profile/profile.component';
import { FeedComponent } from './player/feed/feed.component';
import { CoachProfilComponent } from './coach-profil/coach-profil.component';
import { CoachFeedComponent } from './coach-feed/coach-feed.component';
import { SignUPComponent } from './Auth/sign-up/sign-up.component';
import { SignINComponent } from './Auth/sign-in/sign-in.component';
import { DoctorProfilComponent } from './doctor/doctor-profil/doctor-profil.component';
import { ClubProfilComponent } from './club-profil/club-profil.component';
import { ClubFeedComponent } from './club-feed/club-feed.component';
import {DoctorFeedComponent} from './doctor/doctor-feed/doctor-feed.component';

export const routes: Routes = [
  { path: '', redirectTo: 'recommender', pathMatch: 'full' }, // redirection par défaut
  { path: 'recommender', component: RecommenderComponent },
  { path: 'ronaldo', component: RonaldoProfileComponent },
  { path: 'player/profile', component: ProfileComponent },
  { path: 'player/feed', component: FeedComponent },
  { path: 'coach-feed', component: CoachFeedComponent },
  { path: 'coach-profile', component: CoachProfilComponent },
  { path: 'doctor/doctor-profile', component: DoctorProfilComponent },
  { path: 'doctor/doctor-feed', component: DoctorFeedComponent },
  { path: 'Auth/signUP', component: SignUPComponent },
  { path: 'Auth/signIN', component: SignINComponent },
  { path: 'club-feed', component: ClubFeedComponent },
  { path: 'club-profil', component: ClubProfilComponent } // ✅ corrigé : minuscules uniquement
];
