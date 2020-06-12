import { S3ObjectBokehPlot } from 'src/app/models/s3-object-bokeh-plot';

export interface S3ObjectBokehPlotsGetResponse {
  plots: S3ObjectBokehPlot[];
  length: number;
}
