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
  showPagination = true;

  constructor(protected coreService: CoreService) {}

  ngOnInit() {
    this.coreService.getNumberOfOffers().subscribe(
      data => {
        this.maxPage = Math.ceil(JSON.parse(JSON.stringify(data)).count / 3);
      },
      error => {
        console.error(error.message);
      }
    );

    this.getOffers(0);
  }

  getOffers(pageNo) {
    this.currentPage = pageNo;
    if (this.sortCijena) {
      this.coreService.getOffersByPage(pageNo, 3, '', this.sortAsc).subscribe(
        data => {
          this.offers = data;
        },
        error => {
          console.error(error.message);
        }
      );
    } else {
      this.coreService.getOffersByPage(pageNo, 3).subscribe(
        data => {
          this.offers = data;
        },
        error => {
          console.error(error.message);
        }
      );
    }
  }

  search(event: any) {
    if (event) {
      this.searchQ = event.target.value;
    }
    this.showPagination = this.searchQ === '' || this.searchQ === undefined;
    this.currentPage = 0;

    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      if (this.sortCijena) {
        this.coreService
          .getOffersByPage(
            0,
            this.showPagination ? 3 : 15,
            this.searchQ,
            this.sortAsc
          )
          .subscribe(data => {
            this.offers = data;
          });
      } else {
        this.coreService
          .getOffersByPage(0, this.showPagination ? 3 : 15, this.searchQ)
          .subscribe(data => {
            this.offers = data;
          });
      }
    }, 600);
  }

  orderPrice() {
    this.currentPage = 0;
    this.sortCijena = true;
    this.sortAsc = !this.sortAsc;
  }
}
