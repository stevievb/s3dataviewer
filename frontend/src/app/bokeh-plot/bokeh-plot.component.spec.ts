import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BokehPlotComponent } from './bokeh-plot.component';

describe('BokehPlotComponent', () => {
  let component: BokehPlotComponent;
  let fixture: ComponentFixture<BokehPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BokehPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BokehPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
