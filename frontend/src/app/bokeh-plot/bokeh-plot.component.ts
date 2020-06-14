import { Component, ElementRef, Input, OnInit, AfterViewInit, OnDestroy } from '@angular/core';
import { S3DataViewerBackendService } from 'src/app/services/s3-data-viewer-backend.service';

declare var Bokeh: any;

@Component({
  selector: 'app-bokeh-plot',
  template: `
    <mat-spinner *ngIf="!loaded" color="accent"></mat-spinner>
    <html [id]="this.bokehScriptId"></html>
  `
})

export class BokehPlotComponent implements OnInit, AfterViewInit {
  @Input() bokehScriptId: number;
  @Input() bokehSessionId: string;
  @Input() bokehScriptSrc: string;
  @Input() token: string;

  loaded: boolean = false;
  bokehSessions = [];

  constructor(
    private elementRef: ElementRef,
    private backendService: S3DataViewerBackendService
  ) {}

  ngOnInit(): void {

  }

  ngAfterViewInit(): void {
    this.backendService.getAutolLoadJs(this.bokehScriptSrc, this.bokehSessionId).subscribe(x => this.embedPlot());
  }

  embedPlot(): void {
    const local_url = 'http://' + window.location.hostname + ':5006/image';
    const docs_json = 'null';
    let render_items: Array<any> = [{
      'elementid': this.bokehScriptId.toString(),
      'sessionid': this.bokehSessionId,
      'use_for_title': false,
      'token': this.token
    },];

    Bokeh.embed.embed_items(docs_json, render_items, '/image', local_url).then(plot_data => {
        this.bokehSessions.push(plot_data);
        this.setLoaded();
      });

  }

  setLoaded(): void {
    this.loaded = true;
  }

  ngOnDestroy(): void {

  }
}
