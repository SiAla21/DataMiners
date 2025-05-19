import { Component } from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {WebcamModule} from "ngx-webcam";

@Component({
  selector: 'app-club-profil',
    imports: [
        WebcamModule
    ],
  templateUrl: './club-profil.component.html',
  styleUrl: './club-profil.component.css'
})
export class ClubProfilComponent {

}
