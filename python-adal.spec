%if 0%{?fedora}
%global _with_python3 1
%endif

%global _with_tests 0

%if 0%{?rhel}
%global py2_prefix python
%else
%global py2_prefix python2
%endif

%global srcname adal

%global common_summary ADAL for Python
%global common_description The ADAL for Python library makes it easy for python applications to \
authenticate to AAD in order to access AAD protected web resources.

Name:           python-%{srcname}
Version:        0.6.0
Release:        1%{?dist}
Summary:        %{common_summary}

Group:          System Environment/Libraries
License:        MIT
URL:            https://github.com/AzureAD/azure-activedirectory-library-for-python/
Source0:        %{name}-%{version}.tar.gz
# Fix install_requires option, for EPEL especially
Patch0:         %{name}-0.4.4-build.patch

BuildRequires:  %{py2_prefix}-setuptools
BuildRequires:  python-devel

Requires:       %{py2_prefix}-dateutil
Requires:       %{py2_prefix}-jwt
Requires:       %{py2_prefix}-requests

# Needed for tests
%if 0%{?_with_tests}
BuildRequires:  %{py2_prefix}-cryptography
BuildRequires:  %{py2_prefix}-dateutil
BuildRequires:  python-httpretty
BuildRequires:  %{py2_prefix}-jwt
BuildRequires:  %{py2_prefix}-requests
%if 0%{?_with_python3}
BuildRequires:  python3-devel
# Needed for tests
BuildRequires:  python3-cryptography
BuildRequires:  python3-dateutil
BuildRequires:  python3-httpretty
BuildRequires:  python3-jwt
BuildRequires:  python3-requests
%endif
%endif
BuildArch:      noarch

%description
%{common_description}


%if 0%{?_with_python3}
%package -n python3-%{srcname}
Summary:        %{common_summary}
Requires:       python3-dateutil
Requires:       python3-jwt
Requires:       python3-requests
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{common_description}
%endif


%prep
%autosetup -n azure-activedirectory-library-for-python-%{version} -p1

# Remove BOM
pushd adal/
tail --bytes=+4 __init__.py >__init__.py.new && \
touch -r __init__.py __init__.py.new && \
mv __init__.py.new __init__.py
popd

# Delete tests requiring a valid Azure account
rm tests/{test_client_credentials.py,test_e2e_examples.py}


%build
%py2_build
%{?_with_python3:%py3_build}


%install
%py2_install
%{?_with_python3:%py3_install}


%check
%if 0%{?_with_tests}
%{__python2} setup.py test
%{?_with_python3:%{__python3} setup.py test}
%endif


%files -n python-%{srcname}
%doc README.md
%license LICENSE
%{python2_sitelib}/*


%if 0%{?_with_python3}
%files -n python3-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/*
%endif


%changelog
* Mon May 13 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 0.6.0-1
- Update to 0.6.0
  Resolves: rhbz#1707863

* Sun Sep 03 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.7-1
- Update to 0.4.7
- Use python2- prefix for Fedora dependencies if possible

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.6-1
- Update to 0.4.6

* Wed Mar 01 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.5-1
- Update to 0.4.5

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.4-1
- Update to 0.4.4

* Thu Jan 05 2017 Adam Williamson <awilliam@redhat.com> - 0.4.3-2
- Fix build on Rawhide by loosening a bogus restriction in the deps

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com>
- Rebuild for Python 3.6

* Sun Dec 04 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 20 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.0-2
- Fix build (disable tests requiring a valid Azure account)

* Mon Feb 08 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.0-1
- Initial RPM release
