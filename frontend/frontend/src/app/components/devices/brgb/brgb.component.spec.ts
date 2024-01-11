import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BrgbComponent } from './brgb.component';

describe('BrgbComponent', () => {
  let component: BrgbComponent;
  let fixture: ComponentFixture<BrgbComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BrgbComponent]
    });
    fixture = TestBed.createComponent(BrgbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
