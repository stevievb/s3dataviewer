import { Component, HostListener } from '@angular/core';
import { PageEvent } from '@angular/material';
import { Subscription } from 'rxjs';
import { finalize } from 'rxjs/operators';

import { S3DataViewerBackendService } from 'src/app/services/s3-data-viewer-backend.service';
import { S3ObjectBokehPlot } from 'src/app/models/s3-object-bokeh-plot';

declare var Bokeh: any;

@Component({
  selector: 'home-component',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent {

  // Page Variables
  pageLoading: boolean = false;
  plots: S3ObjectBokehPlot[] = [];

  // Declare height and width variables
  scrHeight: number;
  scrWidth: number;

  // MatPaginator Inputs
  length: number = 0;
  pageSize: number = 12;
  pageIndex: number = 0;
  pageSizeOptions: number[] = [4, 8, 12, 24, 48];

  plotsRequestSubscription: Subscription;

  constructor(private backendService: S3DataViewerBackendService) {
    Bokeh.set_log_level('warn');
    this.getScreenSize();
  }

  searchObjects(bucket, prefix): void {
    this.pageLoading = true;

    this.backendService.buildIndex(bucket, prefix)
      .pipe(finalize(() => this.pageLoading = false))
      .subscribe();
  }

  getPlots(bucket): void {
    this.pageLoading = true;

    if(this.plotsRequestSubscription) {
      this.plotsRequestSubscription.unsubscribe();
    }

    this.plotsRequestSubscription = this.backendService.getPlots(
      bucket,
      this.pageSize,
      this.pageIndex * this.pageSize,
      Math.floor(this.scrHeight / 3  * .6),
      Math.floor(this.scrWidth / 4  * .9),
      true,
      'key',
      ''
    ).subscribe(resp => {
      this.plots = resp.plots;
      this.length = resp.length;

      this.pageLoading = false;
    });
  }

  pageEvent(event: PageEvent, bucket): void {
    this.pageSize = event.pageSize;
    this.pageIndex = event.pageIndex;
    this.getPlots(bucket);
  }

  getAnySelectedImages(): S3ObjectBokehPlot[] {
    return this.plots.filter((image: S3ObjectBokehPlot) => image.selected);
  }

  clearSelection(): void {
    this.plots.forEach((image: S3ObjectBokehPlot) => image.selected = false);
  }

  selectAllImages(): void {
    this.plots.forEach((image: S3ObjectBokehPlot) => image.selected = true);
  }

  copyImages(): void {
    console.log('Should copy:', this.getAnySelectedImages());
  }

  moveImages(): void {
    console.log('Should move:', this.getAnySelectedImages());
  }

  deleteImages(): void {
    console.log('Should delete:', this.getAnySelectedImages());
  }

  @HostListener('window:resize', ['$event'])
  getScreenSize(event?): void {
    this.scrHeight = window.innerHeight;
    this.scrWidth = window.innerWidth;
  }
}