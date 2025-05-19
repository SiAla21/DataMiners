import { Component, OnInit } from '@angular/core';
import { ClubService, ClubDetails, WeaknessResponse } from '../club.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

declare var bootstrap: any;

@Component({
  selector: 'app-club',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './club.component.html'
})
export class ClubComponent implements OnInit {
  clubName = 'Juventus';
  result: string[] = [];
  error = '';
  clubStats: ClubDetails = { club: '' };
  showWeakest = false;

  constructor(private clubService: ClubService) {}

  ngOnInit(): void {}

  showStatsModal(): void {
    this.fetchClubDetails();
    const modal = new bootstrap.Modal(document.getElementById('clubStatsModal'));
    modal.show();
  }

  showWeakestModal(): void {
    this.fetchWeakestPositions();
    const modal = new bootstrap.Modal(document.getElementById('weakestModal'));
    modal.show();
  }

  fetchClubDetails(): void {
    this.error = '';
    this.clubStats = { club: '' };
    this.result = [];
    this.showWeakest = false;

    this.clubService.getClubDetails(this.clubName).subscribe({
      next: (res) => this.clubStats = res,
      error: (err) => this.error = err.error?.error || 'Club not found.'
    });
  }

  fetchWeakestPositions(): void {
    this.error = '';
    this.showWeakest = false;

    this.clubService.getWeakestPositions(this.clubName).subscribe({
      next: (res: WeaknessResponse) => {
        this.result = [...res.top_5_weakest_positions];
        this.showWeakest = true;
      },
      error: (err) => {
        this.error = err.error?.error || 'Prediction failed.';
      }
    });
  }

  statKeys(): string[] {
    return Object.keys(this.clubStats).filter(key => key !== 'club');
  }
}
