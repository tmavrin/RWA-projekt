import { Component, OnInit } from '@angular/core';
import { CoreService } from '../../core/core.service';

@Component({
  selector: 'app-offer',
  templateUrl: './offer.component.html',
  styleUrls: ['./offer.component.scss']
})
export class OfferComponent implements OnInit {
  offers: any;
  pageNo = 0;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.getOffers();
  }

  getOffers() {
    this.coreService.getOffersByPage(this.pageNo).subscribe(
      data => { this.offers = data; },
      error => { console.log(error.message); }
    );
  }
}
