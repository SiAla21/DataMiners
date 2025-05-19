import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DoctorFeedComponent } from './doctor-feed.component';

describe('DoctorFeedComponent', () => {
  let component: DoctorFeedComponent;
  let fixture: ComponentFixture<DoctorFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DoctorFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DoctorFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
