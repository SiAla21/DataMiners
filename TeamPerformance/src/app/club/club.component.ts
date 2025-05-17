import { Component } from '@angular/core';
import { ClubService, ClubDetails, WeaknessResponse } from '../club.service';

@Component({
  selector: 'app-club',
  templateUrl: './club.component.html'
})
export class ClubComponent {
  clubName = '';
  result: string[] = [];
  error = '';
  clubStats: ClubDetails = { club: '' };
  showWeakest = false;

  constructor(private clubService: ClubService) {}

  fetchClubDetails(): void {
    this.error = '';
    this.clubStats = { club: '' };
    this.result = [];
    this.showWeakest = false;

    this.clubService.getClubDetails(this.clubName).subscribe({
      next: (res) => {
        this.clubStats = res;
      },
      error: (err) => {
        this.error = err.error?.error || 'Club not found.';
      }
    });
  }

  fetchWeakestPositions(): void {
    this.error = '';
    this.showWeakest = false;

    this.clubService.getWeakestPositions(this.clubName).subscribe({
      next: (res: WeaknessResponse) => {
        console.log('✅ Received weakest:', res.top_5_weakest_positions);
        this.result = [...res.top_5_weakest_positions]; // force new reference
        this.showWeakest = true;
      },
      error: (err) => {
        console.error('❌ Predict error:', err);
        this.error = err.error?.error || 'Prediction failed.';
      }
    });
  }

  statKeys(): string[] {
    return Object.keys(this.clubStats)
      .filter(key => key !== 'club');
  }
}
