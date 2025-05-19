import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClubProfilComponent } from './club-profil.component';

describe('ClubProfilComponent', () => {
  let component: ClubProfilComponent;
  let fixture: ComponentFixture<ClubProfilComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClubProfilComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClubProfilComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
