import { Component } from '@angular/core';
import {Subject} from "rxjs";
import {WebcamImage, WebcamModule} from "ngx-webcam";
import {Router} from "@angular/router";
import {PlayerService} from '../../player.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,     // ✅ AJOUT INDISPENSABLE
    WebcamModule
  ],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})

export class ProfileComponent {

  showWebcam = false;
  capturedPaths: string[] = [];
  score: number | null = null;
  playerId: number | null = null;
  rawOutput: string = '';
  isVerified: boolean = true;

  private trigger: Subject<void> = new Subject<void>();
  triggerObservable = this.trigger.asObservable();

  constructor(private playerService: PlayerService,  private router: Router ) {}

  startCapture() {
    this.capturedPaths = [];
    this.score = null;
    this.showWebcam = true;
  }

  takeSnapshot() {
    if (this.capturedPaths.length < 3) {
      this.trigger.next();
    }
  }

  cancel() {
    this.showWebcam = false;
    this.capturedPaths = [];
  }

  handleImage(webcamImage: WebcamImage) {
    console.log("📸 Image capturée avec succès", webcamImage); // 👈 AJOUTE ÇA

    const blob = this.dataURLtoBlob(webcamImage.imageAsDataUrl);
    const file = new File([blob], `webcam_${Date.now()}.jpg`, { type: 'image/jpeg' });

    this.playerService.uploadImage(file).subscribe(path => {
      this.capturedPaths.push(path);

      if (this.capturedPaths.length === 3) {
        this.verifyAndCleanup();
      }
    });
  }




  verifyAndCleanup() {
    this.showWebcam = false;
    this.playerId = 1;

    this.playerService.verifyPlayer(this.playerId!, 'Dani Olmo', this.capturedPaths)
      .subscribe({
        next: (result: string) => {
          this.rawOutput = result;

          // Extract score if present
          const match = result.match(/SCORE\s+(\d+)/i);
          this.score = match ? parseInt(match[1]) : null;
        },
        error: err => {
          console.error('Verification failed:', err);
          this.rawOutput = 'Verification error occurred.';
        }
      });
  }
  deleteCapturedImages() {
    this.capturedPaths.forEach(path => {
      this.playerService.deleteImage(path).subscribe({
        next: () => console.log(`Deleted: ${path}`),
        error: err => console.error(`Failed to delete ${path}`, err)
      });
    });

    this.capturedPaths = [];
    console.log("All images deleted.");
  }


  private dataURLtoBlob(dataURL: string): Blob {
    const byteString = atob(dataURL.split(',')[1]);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const intArray = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      intArray[i] = byteString.charCodeAt(i);
    }
    return new Blob([intArray], { type: 'image/jpeg' });
  }
}
