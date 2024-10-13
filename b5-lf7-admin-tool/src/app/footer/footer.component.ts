import { Component, OnInit } from '@angular/core';
import { UpdateWorkerService } from '../update-worker.service';
import { HlmCardDirective, HlmCardHeaderDirective, HlmCardTitleDirective, HlmCardDescriptionDirective, HlmCardContentDirective, HlmCardFooterDirective } from '@spartan-ng/ui-card-helm';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [
    HlmCardDirective,
    HlmCardHeaderDirective,
    HlmCardTitleDirective,
    HlmCardDescriptionDirective,
    HlmCardContentDirective,
    HlmCardFooterDirective,
  ],
  templateUrl: './footer.component.html',
  styles: ``
})
export class FooterComponent implements OnInit {
  countdown: number | null = null;

  constructor(private updateWorkerService: UpdateWorkerService) {}

  ngOnInit(): void {
    this.updateWorkerService.countdown$.subscribe(countdown => {
      this.countdown = countdown; // Update countdown from the service
    });
  }

  fetchDataNow(): void {
    this.updateWorkerService.fetchDataNow(); // Trigger immediate data fetch
  }
}
