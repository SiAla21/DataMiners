import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DoctorProfilComponent } from './doctor-profil.component';

describe('DoctorProfilComponent', () => {
  let component: DoctorProfilComponent;
  let fixture: ComponentFixture<DoctorProfilComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DoctorProfilComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DoctorProfilComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
