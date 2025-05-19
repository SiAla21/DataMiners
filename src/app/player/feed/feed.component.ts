import { Component } from '@angular/core';
import {BlogFormComponent} from '../../shared/blog-form/blog-form.component';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-feed',
  imports: [
    BlogFormComponent,
    DatePipe
  ],
  templateUrl: './feed.component.html',
  styleUrl: './feed.component.css'
})
export class FeedComponent {

  currentUserId = 1;
}
