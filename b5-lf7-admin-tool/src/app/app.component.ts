import { Component, QueryList, ViewChildren } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ParkplatzComponent } from './parkplatz/parkplatz.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from "./footer/footer.component";
import { StatisticsComponent } from "./statistics/statistics.component";
import { UpdateWorkerService } from './update-worker.service';
import { HlmScrollAreaComponent } from '@spartan-ng/ui-scrollarea-helm';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ParkplatzComponent,
    HeaderComponent,
    FooterComponent,
    StatisticsComponent,
    HlmScrollAreaComponent
],
  templateUrl: './app.component.html'
})
export class AppComponent {
  title = 'b5-lf7-admin-tool';
  parkplaetze : any[] = []
  @ViewChildren(ParkplatzComponent) parkplatzComponents!: QueryList<ParkplatzComponent>; // Get references to Parkplatz components

  constructor(public updateWorkerService:UpdateWorkerService) {}

  ngOnInit(): void {
    this.updateWorkerService.data$.subscribe(data => {
      this.parkplaetze = data?.records
    });
  }

  handleStatusChange(newStatus: string): void {
    this.parkplatzComponents.forEach((parkplatz) => {
      parkplatz.onStatusChange(newStatus); // Call the onStatusChange method
    });
  }
}
