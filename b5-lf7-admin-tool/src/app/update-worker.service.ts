import { Injectable } from '@angular/core';
import { BehaviorSubject, interval, Subscription } from 'rxjs';
import { map, startWith, tap } from 'rxjs/operators';
import { DatabaseService } from './database.service';

@Injectable({
  providedIn: 'root'
})
export class UpdateWorkerService {
  private dataSubject = new BehaviorSubject<any>(null);
  data$ = this.dataSubject.asObservable();

  private countdownSubject = new BehaviorSubject<number>(0);
  countdown$ = this.countdownSubject.asObservable();

  private readonly intervalInSeconds = 5; // Change this value to adjust the update interval
  private countdownSubscription: Subscription | null = null; // For countdown management

  constructor(private dbService: DatabaseService) {
    this.startUpdateWorker();
  }

  private startUpdateWorker(): void {
    // Fetch data immediately on start
    this.fetchAndStoreData();
    // Start the countdown
    this.startCountdown();

    // Set up an interval to fetch data every x seconds
    interval(this.intervalInSeconds * 1000).subscribe(() => {
      this.fetchAndStoreData(); // Fetch data regularly
      this.resetCountdown(); // Reset countdown after fetching
    });
  }

  private fetchAndStoreData(): void {
    this.dbService.getAllParkplätze().subscribe(
      (data: any[]) => {
        this.dataSubject.next(data); // Store the latest data
        // Do not reset countdown here, handled in the interval
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }

  private startCountdown(): void {
    this.countdownSubject.next(this.intervalInSeconds); // Set initial countdown value

    // Countdown timer logic
    if (this.countdownSubscription) {
      this.countdownSubscription.unsubscribe(); // Unsubscribe if it exists to prevent memory leaks
    }

    this.countdownSubscription = interval(1000).pipe(
      tap(() => {
        const currentCountdown = this.countdownSubject.getValue();
        if (currentCountdown > 0) {
          this.countdownSubject.next(currentCountdown - 1); // Decrement countdown
        }
      }),
      startWith(0)
    ).subscribe();
  }

  private resetCountdown(): void {
    this.countdownSubject.next(this.intervalInSeconds); // Reset countdown to initial value after fetching
  }

  // Immediately fetch data without affecting the countdown
  fetchDataNow(): void {
    this.dbService.getAllParkplätze().subscribe(
      (data: any[]) => {
        this.dataSubject.next(data); // Store the latest data
        // Do not reset countdown here
      },
      (error) => {
        console.error('Error fetching data:', error);
      }
    );
  }

  // Expose a method for other services to get the latest data
  getCurrentData(): any[] {
    return this.dataSubject.value;
  }
}
