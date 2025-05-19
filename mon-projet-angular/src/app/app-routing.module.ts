import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommenderComponent } from './recommender/recommender.component';
import { RonaldoProfileComponent } from './ronaldo-profile/ronaldo-profile.component';

const routes: Routes = [
  { path: '', redirectTo: 'recommender', pathMatch: 'full' },
  { path: 'recommender', component: RecommenderComponent },
  { path: 'ronaldo', component: RonaldoProfileComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

