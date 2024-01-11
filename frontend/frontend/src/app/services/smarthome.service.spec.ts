import { TestBed } from '@angular/core/testing';

import { SmarthomeService } from './smarthome.service';

describe('SmarthomeService', () => {
  let service: SmarthomeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SmarthomeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
