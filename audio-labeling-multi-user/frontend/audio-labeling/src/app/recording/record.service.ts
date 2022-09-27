import { Injectable } from '@angular/core';

import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, } from 'rxjs/operators';
import { SampleResponse, UploadResponse } from '../types';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class RecordService {

  url = environment.host+"unrecorded_samples/"

  constructor(private http: HttpClient) { }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  getText(n = 1): Observable<SampleResponse> {
    return this.http.get<SampleResponse>(this.url+n)
      .pipe(
        catchError(this.handleError)
      );
  }

  uploadRecording(id: number, recording: Blob, browser: string): Observable<UploadResponse> {
    const fd = new FormData()
    fd.append("file", recording)
    fd.append("id", id.toString())
    fd.append("browser", browser)
    return this.http.post<UploadResponse>(this.url, fd)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteSample(id:number):Observable<UploadResponse> {
    return this.http.delete<UploadResponse>(this.url+id)
  }
}
