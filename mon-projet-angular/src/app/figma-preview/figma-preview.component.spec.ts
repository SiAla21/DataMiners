import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FigmaPreviewComponent } from './figma-preview.component';

describe('FigmaPreviewComponent', () => {
  let component: FigmaPreviewComponent;
  let fixture: ComponentFixture<FigmaPreviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FigmaPreviewComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FigmaPreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
