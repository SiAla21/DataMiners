import { Component } from '@angular/core';
import {BlogFormComponent} from '../shared/blog-form/blog-form.component';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-coach-feed',
  imports: [
    BlogFormComponent,
    DatePipe
  ],
  templateUrl: './coach-feed.component.html',
  styleUrl: './coach-feed.component.css'
})
export class CoachFeedComponent {
  currentUserId = 1;


}
