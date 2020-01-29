import { Component, OnInit } from '@angular/core';
import { CoreService } from '../../core/core.service';

@Component({
  selector: 'app-offer',
  templateUrl: './offer.component.html',
  styleUrls: ['./offer.component.scss']
})
export class OfferComponent implements OnInit {
  offers: any;
  maxPage = 0;
  currentPage = 0;
  searchTimeout;
  sortCijena = false;
  sortAsc = true;
  searchQ: string;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.coreService.getNumberOfOffers().subscribe(data => {
      this.maxPage = Math.ceil(JSON.parse(JSON.stringify(data)).count / 3);
    }, error => { console.log(error.message); });

    this.getOffers(0);
  }

  getOffers(pageNo) {
    this.currentPage = pageNo;
    this.coreService.getOffersByPage(pageNo, 3).subscribe(
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
          .getOffersByPage(0, 3, this.searchQ, this.sortAsc)
          .subscribe(data => {
            this.offers = data;
          });
      } else {
        this.coreService
          .getOffersByPage(0, 3, this.searchQ)
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
