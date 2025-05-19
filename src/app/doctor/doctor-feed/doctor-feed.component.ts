import { Component } from '@angular/core';
import {BlogFormComponent} from '../../shared/blog-form/blog-form.component';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-doctor-feed',
  imports: [
    BlogFormComponent,
    DatePipe
  ],
  templateUrl: './doctor-feed.component.html',
  styleUrl: './doctor-feed.component.css'
})
export class DoctorFeedComponent {
  currentUserId = 1;

}
