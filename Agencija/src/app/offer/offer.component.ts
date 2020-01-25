import { Component, OnInit } from '@angular/core';
import { DUMMY_OFFERS } from '../VO/Offer';
import { OfferService } from '../services/offer.service';

@Component({
  selector: 'app-offer',
  templateUrl: './offer.component.html',
  styleUrls: ['./offer.component.scss']
})
export class OfferComponent implements OnInit {
  offers: any = DUMMY_OFFERS;

  constructor(private offerService: OfferService) {}

  ngOnInit() {
    this.offerService.getAllOffers().subscribe(offers => {
      console.log(offers);
      this.offers = offers;
    });
  }
}
