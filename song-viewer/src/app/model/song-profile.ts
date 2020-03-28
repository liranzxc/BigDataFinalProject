import { Song } from './song'
export interface SongProfile {
    artist: string;
    name: string;
    lyrics: string;  
    size: number;
    emotion: string;
    histogram: object;
  }