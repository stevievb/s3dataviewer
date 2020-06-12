import { TestBed } from '@angular/core/testing';

import { S3DataViewerBackendService } from './s3-image-cloud-backend.service';

describe('S3ImageCloudBackendService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: S3DataViewerBackendService = TestBed.get(S3DataViewerBackendService);
    expect(service).toBeTruthy();
  });
});
