import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { S3ObjectBokehPlotsGetResponse } from 'src/app/models/s3-object-bokeh-plots-get-response';

@Injectable({
    providedIn: 'root'
})

export class S3DataViewerBackendService {

    API_URL = 'http://' + window.location.hostname + ':8080';

    constructor(private http: HttpClient) {
    }

    buildIndex(bucket, prefix): Observable<any> {
        return this.http.put(`${this.API_URL}/index`, {
            bucket: bucket,
            prefix: prefix,
        }, {});
    }

    getPlots(bucket, limit, offset, height, width, access_key, secret_access_key, ascending?, sort?, filter_regex?): Observable<S3ObjectBokehPlotsGetResponse> {

        const httpOptions = {
            params: new HttpParams().set('limit', limit).set('offset', offset).set('height',
                height).set('width', width), // Create new HttpParams

        };

        return this.http.get<S3ObjectBokehPlotsGetResponse>(`${this.API_URL}/plots`, httpOptions);
    }

    getAutolLoadJs(scriptSrc, session_id) {
        let heades = new HttpHeaders();//.append("Access-Control-Allow-Origin","*");
        return this.http.get(scriptSrc + '&bokeh-session-id=' + session_id, {headers: heades, responseType: 'text'});
    }
}
