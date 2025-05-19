import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClubFeedComponent } from './club-feed.component';

describe('ClubFeedComponent', () => {
  let component: ClubFeedComponent;
  let fixture: ComponentFixture<ClubFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClubFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClubFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
