import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CategoryHomeComponent } from './home/Category-home.component';
import { CategoryNewComponent } from './new/Category-new.component';
import { CategoryDetailComponent } from './detail/Category-detail.component';

const routes: Routes = [
  {path: '', component: CategoryHomeComponent},
  { path: 'new', component: CategoryNewComponent },
  { path: ':id', component: CategoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Category-detail-permissions'
      }
    }
  },{
    path: ':category_id/ProductCategory', loadChildren: () => import('../ProductCategory/ProductCategory.module').then(m => m.ProductCategoryModule),
    data: {
        oPermission: {
            permissionId: 'ProductCategory-detail-permissions'
        }
    }
}
];

export const CATEGORY_MODULE_DECLARATIONS = [
    CategoryHomeComponent,
    CategoryNewComponent,
    CategoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CategoryRoutingModule { }