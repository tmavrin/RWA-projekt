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

  searchTimeout;
  sortCijena = false;
  sortAsc = true;
  searchQ: string;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.getOffers();
  }

  getOffers() {
    this.coreService.getOffersByPage(this.pageNo).subscribe(
      data => {
        this.offers = data;
      },
      error => {
        console.log(error.message);
      }
    );
  }

  search(event: any) {
    if (event) {
      this.searchQ = event.target.value;
    }
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      if (this.sortCijena) {
        this.coreService
          .getOffersByPage(this.pageNo, 10, this.searchQ, this.sortAsc)
          .subscribe(data => {
            this.offers = data;
          });
      } else {
        this.coreService
          .getOffersByPage(this.pageNo, 10, this.searchQ)
          .subscribe(data => {
            this.offers = data;
          });
      }
    }, 600);
  }

  orderPrice() {
    this.sortCijena = true;
    this.sortAsc = !this.sortAsc;
  }
}
