import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayDeviceComponent } from './display-device.component';

describe('DisplayDeviceComponent', () => {
  let component: DisplayDeviceComponent;
  let fixture: ComponentFixture<DisplayDeviceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DisplayDeviceComponent]
    });
    fixture = TestBed.createComponent(DisplayDeviceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
