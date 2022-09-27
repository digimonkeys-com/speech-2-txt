export interface UploadResponse {
    info: string
}

export interface Sample  {
    id: number,
    transcription: string,
    filename: string
}

export interface SampleResponse{
    samples: Sample[]

}

export interface Status{
    duration: number
    samples: number
    unrecorded_samples: number,
    recorded_samples: number
}