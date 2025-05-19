import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RonaldoProfileComponent } from './ronaldo-profile.component';

describe('RonaldoProfileComponent', () => {
  let component: RonaldoProfileComponent;
  let fixture: ComponentFixture<RonaldoProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RonaldoProfileComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RonaldoProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
