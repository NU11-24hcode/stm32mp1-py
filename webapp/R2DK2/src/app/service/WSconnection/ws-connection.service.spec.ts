import { TestBed } from '@angular/core/testing';

import { WsConnectionService } from './ws-connection.service';

describe('WsConnectionService', () => {
  let service: WsConnectionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WsConnectionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
