import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HouseAlarmComponent } from './house-alarm.component';

describe('HouseAlarmComponent', () => {
  let component: HouseAlarmComponent;
  let fixture: ComponentFixture<HouseAlarmComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HouseAlarmComponent]
    });
    fixture = TestBed.createComponent(HouseAlarmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
