import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DhtComponent } from './dht.component';

describe('DhtComponent', () => {
  let component: DhtComponent;
  let fixture: ComponentFixture<DhtComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DhtComponent]
    });
    fixture = TestBed.createComponent(DhtComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
