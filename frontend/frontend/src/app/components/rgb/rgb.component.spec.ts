import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RgbComponent } from './rgb.component';

describe('RgbComponent', () => {
  let component: RgbComponent;
  let fixture: ComponentFixture<RgbComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RgbComponent]
    });
    fixture = TestBed.createComponent(RgbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
