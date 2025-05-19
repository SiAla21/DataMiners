import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CoachFeedComponent } from './coach-feed.component';

describe('CoachFeedComponent', () => {
  let component: CoachFeedComponent;
  let fixture: ComponentFixture<CoachFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CoachFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CoachFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
