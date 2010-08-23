#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	kitchen
%define		subver	a2
%define		rel		1
Summary:	Small, useful pieces of code to make Python coding easier
Name:		python-%{module}
Version:	0.2
Release:	0.%{subver}.%{rel}
License:	LGPL v2+
Group:		Development/Languages
URL:		https://fedorahosted.org/kitchen/
Source0:	https://fedorahosted.org/releases/k/i/kitchen/%{module}-%{version}%{subver}.tar.gz
# Source0-md5:	54eb68eacf4df9f910aa7533399c986a
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-chardet
BuildRequires:	python-coverage
BuildRequires:	python-nose
%endif
Requires:	python-chardet
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kitchen includes functions to make gettext easier to use, handling
unicode text easier (conversion with bytes, outputting xml, and
calculating how many columns a string takes), and compatibility
modules for writing code that uses python-2.7 modules but needs to run
on python-2.3

%prep
%setup -q -n %{module}-%{version}%{subver}

# can't find origin of this import
grep -r 'from test import test_support' tests -l | xargs rm

%build
%{__python} setup.py build

%if %{with tests}
nosetests --with-coverage --cover-package kitchen
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README NEWS COPYING.LESSER docs
%{py_sitescriptdir}/kitchen/*.py[co]
%{py_sitescriptdir}/kitchen/collections
%{py_sitescriptdir}/kitchen/i18n
%{py_sitescriptdir}/kitchen/pycompat24
%{py_sitescriptdir}/kitchen/pycompat25
%{py_sitescriptdir}/kitchen/pycompat27
%{py_sitescriptdir}/kitchen/text
%{py_sitescriptdir}/kitchen/versioning
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/kitchen-%{version}*.egg-info
%endif
