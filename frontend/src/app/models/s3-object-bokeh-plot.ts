import { S3Object } from 'src/app/models/s3-object';

export interface S3ObjectBokehPlot extends S3Object{
  bokeh_tag: string;
  script_src: string;
  script_id: number;
  session_id: string;
  selected: boolean;
  token: string;
}


