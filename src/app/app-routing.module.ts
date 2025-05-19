import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommenderComponent } from './recommender/recommender.component';
import { RonaldoProfileComponent } from './ronaldo-profile/ronaldo-profile.component';
import {ProfileComponent} from './player/profile/profile.component';
import {FeedComponent} from './player/feed/feed.component';
import {SignINComponent} from './Auth/sign-in/sign-in.component';
import {SignUPComponent} from './Auth/sign-up/sign-up.component';
import {DoctorFeedComponent} from './doctor/doctor-feed/doctor-feed.component';
import {CoachFeedComponent} from './coach-feed/coach-feed.component';
import {CoachProfilComponent} from './coach-profil/coach-profil.component';
import {DoctorProfilComponent} from './doctor/doctor-profil/doctor-profil.component';
import {ClubFeedComponent} from './club-feed/club-feed.component';
import {ClubProfilComponent} from './club-profil/club-profil.component';

const routes: Routes = [
  { path: '', redirectTo: 'recommender', pathMatch: 'full' },
  { path: 'recommender', component: RecommenderComponent },
  { path: 'ronaldo', component: RonaldoProfileComponent },
  { path: 'player/feed', component: FeedComponent },
  { path: 'player/profile', component: ProfileComponent },
  { path: 'Auth/signUP', component: SignUPComponent },
  { path: 'Auth/signIN', component: SignINComponent },
  { path: 'doctor/doctor-profil', component: DoctorProfilComponent  },
  { path: 'doctor/doctor-feed', component: DoctorFeedComponent },
  { path: 'coach/coach-feed', component: CoachFeedComponent },
  { path: 'coach/coach-profil', component: CoachProfilComponent },
  { path: 'club-feed', component: ClubFeedComponent },
  { path: 'club-profil', component: ClubProfilComponent }



];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

