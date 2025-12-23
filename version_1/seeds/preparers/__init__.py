"""Data perparers for seeding."""

from seeds.preparers.policy import PolicyPreparer
from seeds.preparers.role import RolePreparer
from seeds.preparers.permission import PermissionPreparer

PREPARERS = {
    "policies": PolicyPreparer(),
    "roles": RolePreparer(),
    "permissions": PermissionPreparer()
}

__all__ = ['PREPARERS', 'PolicyPreparer', 'RolePreparer', 'PermissionPreparer']
