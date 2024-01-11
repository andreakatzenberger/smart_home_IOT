import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HouseStatusComponent } from './house-status.component';

describe('HouseStatusComponent', () => {
  let component: HouseStatusComponent;
  let fixture: ComponentFixture<HouseStatusComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HouseStatusComponent]
    });
    fixture = TestBed.createComponent(HouseStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
