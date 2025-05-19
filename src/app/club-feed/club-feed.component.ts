import { Component } from '@angular/core';
import {BlogFormComponent} from '../shared/blog-form/blog-form.component';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-club-feed',
  imports: [
    BlogFormComponent,
    DatePipe
  ],
  templateUrl: './club-feed.component.html',
  styleUrl: './club-feed.component.css'
})
export class ClubFeedComponent {
  currentUserId = 1;


}
